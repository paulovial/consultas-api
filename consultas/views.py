from rest_framework import viewsets, filters
from .models import ProfissionalSaude, Consulta
from .serializers import ProfissionalSaudeSerializer, ConsultaSerializer

class ProfissionalSaudeViewSet(viewsets.ModelViewSet):
    queryset = ProfissionalSaude.objects.all()
    serializer_class = ProfissionalSaudeSerializer

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()    
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        profissional_id = self.request.query_params.get('profissional')
        if profissional_id:
            return Consulta.objects.filter(profissional_id=profissional_id)
        return Consulta.objects.all()
