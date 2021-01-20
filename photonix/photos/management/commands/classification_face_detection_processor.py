from django.core.management.base import BaseCommand
# Pre-load the model graphs so it doesn't have to be done for each job
from photonix.classifiers.face_detection import FaceDetectionModel, run_on_photo
from photonix.photos.models import Task
from photonix.photos.utils.classification import ThreadedQueueProcessor


print('Loading face detection  model')
model = FaceDetectionModel()


class Command(BaseCommand):
    help = 'Runs the workers with the face detection model.'

    def run_processors(self):
        num_workers = 4
        batch_size = 64
        threaded_queue_processor = ThreadedQueueProcessor(model, 'classify.face_detection', run_on_photo, num_workers, batch_size)
        threaded_queue_processor.run()

    def handle(self, *args, **options):
        self.run_processors()