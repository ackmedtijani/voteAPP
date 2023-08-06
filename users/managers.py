from django.contrib.auth.models import BaseUserManager 

class CustomUserManager(BaseUserManager):
    
    def _create_user(self, email, name ,  password, **extra_fields):
            if not email:
                raise ValueError("An email has to be set")

            user = self.model(name = name , email=self.normalize_email(email), **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

            return user
    
    
    def create_superuser(self, email, name,  password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, name, password, **extra_fields)
