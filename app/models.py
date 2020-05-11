from django.db import models
from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth.models import User

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/contact_pics/user-<id>-<filename>
    # upload_to='documents/%Y/%m/%d/'
    return f'contact_pics/user-{instance.manager.id}_contact-{str(instance.id)}_{filename}'


class Contacts(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    info = models.CharField(max_length=30)
    gender = models.CharField(max_length=50, choices=(
        ('male', 'Male'),
        ('female', 'Female')
    ))
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    date_added = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name}'s contact"

    class Meta:
        ordering = ['-id']
        verbose_name_plural = "contacts"  # A human-readable name for the object, plural
        verbose_name = "contact"  # A human-readable name for the object, singular

    # Model Save override
    # did this because a picture is not saved before giving it a name, and hence returns None.
    # So, saving it first solves it and hence we can then get the saved contact id

    '''
        Django admin somehow called the user_directory_path function without saving the model to database so id is None. 
        We can override django model using save method and make sure image is saved and user_directory_path get the 
        instance with id
    '''

    def save(self, *args, **kwargs):
        if self.id is None:
            image = self.image
            self.image = None
            super(Contacts, self).save(*args, **kwargs)
            self.image = image
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        # resizing image operation
        im = Image.open(self.image)
        output = BytesIO()
        im = im.resize((250, 130))  # Resize/modify the image
        im.save(output, format='JPEG', quality=100)  # after modifications, save it to the output
        output.seek(0)
        # change the imagefield value to be the newley modifed image value
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                          sys.getsizeof(output), None)

        super(Contacts, self).save(*args, **kwargs)
