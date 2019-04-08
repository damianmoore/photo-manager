import queue
import threading
from time import sleep

from django.db import transaction
from django.utils import timezone
from photonix.photos.models import Task
from photonix.photos.utils.tasks import requeue_stuck_tasks

CLASSIFIERS = [
    'color',
    'location',
    'object',
    'style',
]


def process_classify_images_tasks():
    for task in Task.objects.filter(type='classify_images', status='P').order_by('created_at'):
        photo_id = task.subject_id
        generate_classifier_tasks_for_photo(photo_id, task)


def generate_classifier_tasks_for_photo(photo_id, task):
    task.start()
    started = timezone.now()

    # Add task for each classifier on current photo
    with transaction.atomic():
        for classifier in CLASSIFIERS:
            Task(type='classify.{}'.format(classifier), subject_id=photo_id, parent=task).save()
        task.complete_with_children = True
        task.save()


class ThreadedQueueProcessor:
    def __init__(self, model=None, task_type=None, runner=None, num_workers=4, batch_size=64):
        self.model = model
        self.task_type = task_type
        self.runner = runner
        self.num_workers = num_workers
        self.batch_size = batch_size
        self.queue = queue.Queue()
        self.threads = []

    def __worker(self):
        while True:
            task = self.queue.get()

            if task is None:
                break

            self.__process_task(task)

            self.queue.task_done()

    def __process_task(self, task):
        try:
            print('running task')
            task.start()
            self.runner(task.subject_id)
            task.complete()
        except:
            task.failed()

    def __clean_up(self):
        # Shut down threads cleanly
        for i in range(self.num_workers):
            self.queue.put(None)
        for t in self.threads:
            t.join()

    def run(self, loop=True):
        print('Starting {} {} workers\n'.format(self.num_workers, self.task_type))

        if self.num_workers > 1:
            for i in range(self.num_workers):
                t = threading.Thread(target=self.__worker)
                t.start()
                self.threads.append(t)

        try:
            while True:
                requeue_stuck_tasks(self.task_type)

                for task in Task.objects.filter(type=self.task_type, status='P')[:64]:
                    if self.num_workers > 1:
                        print('putting task')
                        self.queue.put(task)
                    else:
                        self.__process_task(task)

                if self.num_workers > 1:
                    self.queue.join()

                if not loop:
                    self.__clean_up()
                    return
                sleep(1)

        except KeyboardInterrupt:
            self.__clean_up()