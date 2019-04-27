from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
# Resize image on S3
import io
from django.core.files.storage import default_storage as storage



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, null=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img_read = storage.open(self.image.name, 'r')
		img = Image.open(img_read)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			in_mem_file = io.BytesIO()
			img.save(in_mem_file, format='JPEG')
			img_write = storage.open(self.image.name, 'w+')
			img_write.write(in_mem_file.getvalue())
			img_write.close()

		img_read.close()

	# def save_png(self, *args, **kwargs):
	# 	super().save_png(*args, **kwargs)

	# 	img_read.close()

	# 	fill_color = 'white'
	# 	image = Image.open(file_path)
		
	# 	if image.mode in ('RGBA', 'LA'):
	# 	    background = Image.new(image.mode[:-1], image.size, fill_color)
	# 	    background.paste(image, image.split()[-1])
	# 	    image = background
	# 	im.save(hidpi_path, file_type, quality=95)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	'''
	For every new user created, send the properties from Profile.
	'''
	if created:
		Profile.objects.create(user=instance)
	else:
		instance.profile.save()


class Friend(models.Model):
	''' 
	Add & Remove a Friend.
	'''
	friend_user = models.ManyToManyField(User)									# All the people you are friends with
	current_user = models.ForeignKey(User, 
									on_delete=models.CASCADE,
									related_name="owner", 
									null=True)									# Current user browsing the website

	@classmethod
	def make_friend(cls, current_user, new_friend):
		friend, created = cls.objects.get_or_create(							# Create new user
				current_user=current_user										# Assign the new user
			)
		friend.friend_user.add(new_friend)										# Add the new user to M2M

	@classmethod
	def lose_friend(cls, current_user, new_friend):
		friend, created = cls.objects.get_or_create(							# Create new user
				current_user=current_user										# Assign the new user
			)
		friend.friend_user.remove(new_friend)										# Add the new user to M2M


