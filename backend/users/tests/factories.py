import factory
from factory.fuzzy import FuzzyChoice

from users.models import User


class UserFactory(factory.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = "user"
    is_staff = False
    is_active = True
    is_manager = FuzzyChoice(choices=[True, False])

    class Meta:
        model = User

    @factory.lazy_attribute
    def email(self):
        return "{first_name}@example.com".format(first_name=self.first_name)

    @factory.lazy_attribute
    def avatar(self):
        return "https://api.adorable.io/avatars/40/{}".format(self.email)

    @factory.lazy_attribute_sequence
    def first_name(self, seq):
        prefix = "manager" if self.is_manager else "worker"
        return "{prefix}{seq}".format(prefix=prefix, seq=seq)

    @factory.post_generation
    def password(user, create, extracted, **kwargs):
        user.set_password('password')
        user.save()