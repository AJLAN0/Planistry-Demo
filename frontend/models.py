from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    recommended_study_time = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class StudyWeek(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='weeks')
    number = models.PositiveIntegerField()
    topics = models.TextField()
    tasks = models.TextField()
    resources = models.TextField()
    tips = models.TextField()
    
    class Meta:
        ordering = ['number']
    
    def __str__(self):
        return f"Week {self.number} - {self.course.name}"

class Deliverable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='deliverables')
    name = models.CharField(max_length=200)
    week = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} (Week {self.week})"

class EvaluationItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='evaluation')
    name = models.CharField(max_length=200)
    percentage = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} ({self.percentage}%)"