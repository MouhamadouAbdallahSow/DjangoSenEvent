# from django.db import models
# from django.contrib.auth.models import User
# from authentication.models import CustomUser
# from django.conf import settings


# # Create your models here.

# class Testimonial(models.Model):
#     commentaire = models.TextField()
#     evaluation = models.IntegerField(blank=False, null=True)
#     date = models.DateField(auto_now_add=True, blank=True)
#     utilisateur = models.OneToOneField(
#         CustomUser,
#         on_delete=models.CASCADE,
#     )

#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(evaluation__gte=1) & models.Q(evaluation__lte=5),
#                 name="evaluation_between_1_and_5",
#             )
#         ]

#     def __str__(self):
#         return f"Témoignage de {self.utilisateur.username} (Évaluation: {self.evaluation})"