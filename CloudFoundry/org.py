import json

from cloudfoundry.space import Space


class Org:

    def __init__(self, guid, client):
        self.guid = guid
        self.client = client

    def get_space(self, name):
        """ Get a space """
        params = {
            'q': 'name:%s' % name
        }
        endpoint = '/v2/organizations/%s/spaces' % self.guid
        cf_space_res = self.client.api_request(endpoint, params=params).json()
        resources = cf_space_res.get('resources', [])
        if len(resources) == 1:
            return Space(
                guid=resources[0]['metadata']['guid'], client=self.client
            )

    def create_space(self, name):
        """ Create a space within this org """
        data = {
            "name": name,
            "organization_guid": self.guid
        }
        cf_space_res = self.client.api_request(
            endpoint='/v2/spaces', method='post', data=json.dumps(data)
        ).json()
        if 'error_code' not in cf_space_res:
            return Space(
                guid=cf_space_res['metadata']['guid'], client=self.client
            )

    def delete(self):
        api_delete_endpoint = '/v2/organizations/%s' % self.guid
        return self.client.api_request(
            endpoint=api_delete_endpoint, method='delete'
        )

    def set_user_role(self, role, user_guid):
        """ Give a user a specific role """
        endpoint = '/v2/organizations/{0}/{1}/{2}'.format(
            self.guid, role + 's', user_guid
        )
        return self.client.api_request(endpoint=endpoint, method='put')

    def unset_user_role(self, role, user_guid):
        endpoint = '/v2/organizations/{0}/{1}/{2}'.format(
            self.guid, role + 's', user_guid
        )
        return self.client.api_request(endpoint=endpoint, method='delete')

    def update(self, name=None, status=None, quota_definition_guid=None):
        """ Update an organizations name, status, or quota definition  """
        data = {}
        if name:
            data['name'] = name
        if name:
            data['status'] = status
        if name:
            data['quota_definition_guid'] = quota_definition_guid
        endpoint = '/v2/organizations/%s' % self.guid
        self.client.api_request(
            endpoint=endpoint,
            method='put',
            data=json.dumps(data)
        )
