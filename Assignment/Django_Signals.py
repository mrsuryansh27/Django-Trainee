##Django Signals

#Question 1: By default are Django signals executed synchronously or asynchronously?
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def slow_signal_handler(sender, instance, **kwargs):
    print("Signal received!")
    time.sleep(5)
    print("Signal processing finished!")

User.objects.create(username="test_user", email="test@example.com")
print("User created!")


#Question 2: Do Django signals run in the same thread as the caller?
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def check_thread(sender, instance, **kwargs):
    print(f"Signal received on thread: {threading.current_thread().name}")

def create_user():
    print(f"User creation on thread: {threading.current_thread().name}")
    User.objects.create(username="thread_test_user", email="threadtest@example.com")

create_user()


#Question 3: By default do Django signals run in the same database transaction as the caller?
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def signal_handler(sender, instance, **kwargs):
    print(f"Signal: User {instance.username} created in transaction.")

def create_user_with_transaction():
    try:
        with transaction.atomic():
            user = User.objects.create(username="transaction_user", email="transaction@example.com")
            print("User created inside transaction.")
            raise Exception("Simulate an error, rollback transaction!")
    except Exception as e:
        print(f"Transaction rolled back: {e}")

create_user_with_transaction()
print(User.objects.filter(username="transaction_user").exists())
