from django.core.management.base import BaseCommand
# Pre-load the model graphs so it doesn't have to be done for each job
from photonix.classifiers.object import ObjectModel, run_on_photo
from photonix.photos.models import Task
from photonix.photos.utils.classification import ThreadedQueueProcessor


print('Loading object classification model')
model = ObjectModel()


class Command(BaseCommand):
    help = 'Runs the workers with the object classification model.'

    def run_processors(self):
        num_workers = 1
        batch_size = 64
        threaded_queue_processor = ThreadedQueueProcessor(model, 'classify.object', run_on_photo, num_workers, batch_size)
        threaded_queue_processor.run()

    def handle(self, *args, **options):
        self.run_processors()
