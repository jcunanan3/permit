from django.db import models
from django.contrib.auth.models import AbstractUser
from permit_app.helpers import get_lat_lng


# Create your models here.
class PermitUser(AbstractUser):
    # Why do users have address fields? Do we care, or do we only care about the Permit address fields?
    phone = models.CharField(max_length=12, help_text="Format should be: 415-111-2222")
    address_1 = models.CharField(("address1"),max_length=128)
    address_2 = models.CharField(("address2"),max_length=128, blank=True)
    city = models.CharField(("city"), max_length=64, default="San Francisco")
    state = models.CharField(max_length=2, default="CA")
    zip_code = models.CharField(("zip code"), max_length=5, default="94133")
    MTA_staff=models.BooleanField(default=False)


class Permit(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=30,default="San Francisco")
    state = models.CharField(max_length=2,default="CA")
    zip = models.IntegerField()
    date = models.DateField()
    # By having both `approved` and `rejected` fields, a permit could be both approved and rejected, which
    # doesn't make a lot of sense
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    user = models.ForeignKey(PermitUser)
    resident_comments = models.TextField()
    MTA_comments = models.TextField()
    # latlng= models.CharField((u'Latitude/Longitude'), blank=True, max_length=100, help_text=(u'Note: This field will be filled-in automatically based on the other address bits.'))
    #
    # class Meta:
    #     abstract = True
    #
    # def save(self):
    #     if not self.latlng:
    #         location = '+'.join(filter(None, (self.street_address, self.city, self.state, self.zip, )))
    #         self.latlng = get_lat_lng(location)
    #     super(Permit,self).save()


    # def __unicode__(self):
    #     return self.user
