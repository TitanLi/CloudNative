
import base64
import jinja2
import json
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.policy import Policy

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))


class ServiceOneInstancePolicy(Policy):
    model_name = "TestInstance"

    def handle_create(self, service_instance):
        return self.handle_update(service_instance)

    def handle_update(self, service_instance):
        compute_service = KubernetesService.objects.first()
        compute_service_instance_class = Service.objects.get(id=compute_service.id).get_service_instance_class()
        slice = Slice.objects.filter(name="test")[0]
        image = Image.objects.filter(name="mysql")[0]
        name="serviceone-%s" % service_instance.id
        instance = compute_service_instance_class(slice=slice, owner=compute_service, image=image, name=name, no_sync=False)

        instance.save()

    def handle_delete(self, service_instance):
        log.info("handle_delete")
        log.info("has a compute_instance")
        service_instance.compute_instance.delete()
        service_instance.compute_instance = None
        # TODO: I'm not sure we can save things that are being deleted...
        service_instance.save(update_fields=["compute_instance"])