import os
import sys
import json
from django.core.management import execute_from_command_line
from django.apps import apps
from django.core.serializers import serialize
from django.utils.encoding import smart_str


# Функция для сериализации данных моделей и сохранения их в файл
def serialize_models_to_file():
    # Получение списка всех моделей
    all_models = apps.get_models()

    # Сериализация данных всех моделей
    serialized_data = []
    for model in all_models:
        serialized_data += json.loads(serialize('json', model.objects.all()))

    # Кодировка для сохранения данных
    output_encoding = 'utf-16'

    # Имя файла для сохранения данных
    output_filename = 'all_models_fixture.json'

    # Сохранение сериализованных данных в файл
    with open(output_filename, 'w', encoding=output_encoding) as output_file:
        for obj in serialized_data:
            output_file.write(smart_str(json.dumps(obj, ensure_ascii=False)))
            output_file.write('\n')


# Запускаем Django только после того, как вызвана наша функция
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sportservice.settings")

    # Сериализуем модели и сохраняем их в файл
    serialize_models_to_file()

    # Выполняем команды Django
    execute_from_command_line(sys.argv)
