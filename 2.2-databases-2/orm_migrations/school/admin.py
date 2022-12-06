from django.contrib import admin

from .models import Student, Teacher


class StudentTeachersInline(admin.TabularInline):
    model = Student.teachers.through
    extra = 1


class TeacherStudents(admin.StackedInline):
    model = Teacher.students.through


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group',)
    list_filter = ('group', )
    inlines = [
        StudentTeachersInline,
    ]
    exclude = ('teachers',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject')
    list_filter = ('subject',)
    inlines = [
        TeacherStudents,
    ]
    exclude = ('students',)

