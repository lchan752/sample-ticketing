{{/* get configmap hash */}}
{{- define "backend.get_configmap_hash" }}
{{- include (print $.Template.BasePath "/backend/configmap.yaml") . | sha256sum }}
{{- end }}

{{/* get image */}}
{{- define "backend.get_image" }}
{{- printf "%v:%v" .image .tag | quote }}
{{- end }}

{{/* get environs */}}
{{- define "backend.get_environs" }}
envFrom:
- configMapRef:
    name: {{ .Release.Name }}-backend
env:
- name: DB_PWD
  valueFrom:
    secretKeyRef:
      name: {{ .Release.Name }}-postgresql
      key: postgres-password
{{- end }}

{{/* get volumes */}}
{{- define "backend.get_volumes" }}
volumes:
- name: {{ .Release.Name }}-ticketing
  persistentVolumeClaim:
    claimName: {{ .Release.Name }}-backend
{{- end }}

{{/* get volume mounts */}}
{{- define "backend.get_volume_mounts" }}
volumeMounts:
- name: {{ .Release.Name }}-ticketing
  mountPath: /pv/
{{- end }}