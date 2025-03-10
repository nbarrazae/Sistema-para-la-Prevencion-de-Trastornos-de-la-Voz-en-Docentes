from rest_framework import serializers
from .models import Institucion, Profesor, Aula, Horario

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['rut_institucion', 'nombre_institucion', 'direccion', 'sitio_web', 'representante_legal', 'telefono_institucion', 'correo_institucion']


class ProfesorSerializer(serializers.ModelSerializer):
    id_institucion = serializers.SlugRelatedField(
        queryset=Institucion.objects.all(), slug_field='nombre_institucion'
    )
    
    class Meta:
        model = Profesor
        fields = ['rut_profesor', 'nombre_profesor', 'apellido_profesor', 'correo_profesor', 'sexo', 'altura', 'peso', 'antecedentes_medicos', 'area_docencia', 'id_institucion']

class AulaSerializer(serializers.ModelSerializer):
    id_institucion = serializers.SlugRelatedField(
        queryset=Institucion.objects.all(), slug_field='rut_institucion'
    )
    
    class Meta:
        model = Aula
        fields = ['nro_aula', 'tamaño', 'cantidad_alumnos', 'descripcion', 'id_institucion']

class HorarioSerializer(serializers.ModelSerializer):
    id_profesor = serializers.SlugRelatedField(
        queryset=Profesor.objects.all(), slug_field='rut_profesor'
    )
    aula = serializers.SerializerMethodField()  # Renombramos a "aula" para evitar conflictos con "id_aula"

    class Meta:
        model = Horario
        fields = ['dia', 'hora_inicio', 'hora_termino', 'id_profesor', 'aula']

    def get_aula(self, obj):
        return {
            "nro_aula": obj.id_aula.nro_aula,
            "nombre_institucion": obj.id_aula.id_institucion.nombre_institucion
        }

    def create(self, validated_data):
        request_data = self.context['request'].data
        try:
            profesor = Profesor.objects.get(rut_profesor=request_data['id_profesor'])
            aula_data = request_data.get('id_aula', {})
            aula = Aula.objects.get(
                nro_aula=aula_data.get('nro_aula'),
                id_institucion__nombre_institucion=aula_data.get('nombre_institucion')
            )
        except Profesor.DoesNotExist:
            raise serializers.ValidationError("El profesor especificado no existe")
        except Aula.DoesNotExist:
            raise serializers.ValidationError("El aula especificada no existe")

        validated_data['id_profesor'] = profesor
        validated_data['id_aula'] = aula
        return super().create(validated_data)
