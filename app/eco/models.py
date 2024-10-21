from django.db import models


wastes = ['bio', 'glass', 'plastic']
class Building(models.Model):
    coord_x = models.FloatField()
    coord_y = models.FloatField()
    cur_bio = models.FloatField(default=0.0)
    cur_glass = models.FloatField(default=0.0)
    cur_plastic = models.FloatField(default=0.0)
    name = models.CharField(max_length=200)

    def get_coords(self):
        return self.coord_x, self.coord_y

    def get_waste(self):
        return {"bio": self.cur_bio, "glass": self.cur_glass, "plastic": self.cur_plastic}

    def get_name(self):
        return self.name

    class Meta:
        abstract = True


class Organization(Building):

    def generate(self, waste_type: str, amount: float):
        if waste_type not in wastes:
            return False
        if waste_type == 'bio':
            self.cur_bio += amount
        elif waste_type == 'glass':
            self.cur_glass += amount
        elif waste_type == 'plastic':
            self.cur_plastic += amount
        return True

    def send_to_storage(self, waste_type: str, amount: float):
        if waste_type not in wastes:
            return False, "Waste type is incorrect"
        if waste_type == 'bio':
            if (self.cur_bio - amount) < 0:
                return False, "Amount is incorrect"
            self.cur_bio -= amount
        elif waste_type == 'glass':
            if (self.cur_glass - amount) < 0:
                return False, "Amount is incorrect"
            self.cur_glass -= amount
        elif waste_type == 'plastic':
            if (self.cur_plastic - amount) < 0:
                return False, "Amount is incorrect"
            self.cur_plastic -= amount
        return True


class Storage(Building):
    max_bio = models.FloatField()
    max_glass = models.FloatField()
    max_plastic = models.FloatField()

    def get_free_space(self):
        return {'bio': self.max_bio - self.cur_bio,
                'glass': self.max_glass - self.cur_glass,
                'plastic': self.max_plastic - self.cur_plastic}

    def store(self, waste_type: str, amount: float):
        if waste_type not in wastes:
            return False
        free_space = self.get_free_space()
        if free_space[waste_type] < amount:
            return False
        if waste_type == 'bio':
            self.cur_bio += amount
        elif waste_type == 'glass':
            self.cur_glass += amount
        elif waste_type == 'plastic':
            self.cur_plastic += amount
        return True
