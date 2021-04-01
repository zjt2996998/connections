# -*- mode: Python -*-

k8s_yaml(['deploy/mysql.yaml', 'deploy/connections.yaml', 'deploy/jobs.yaml'])
k8s_resource('connections', port_forwards='5000:80')


docker_build('connections-image', '.', build_args={'flask_env': 'development'})
