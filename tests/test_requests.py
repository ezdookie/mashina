def test_crud(falcon_client):
    # testing create
    result = falcon_client.simulate_post('/todos', json={
        'name': 'testing'
    })
    assert result.status_code == 200
    assert 'name' in result.json

    # testing list
    result = falcon_client.simulate_get('/todos')
    assert result.status_code == 200
    assert result.json['count'] == 1

    # testing retrieve
    todo_id = result.json['results'][0]['id']
    todo_url = '/todos/%s' % todo_id
    result = falcon_client.simulate_get(todo_url)
    assert result.status_code == 200
    assert result.json['id'] == todo_id

    # testing update
    result = falcon_client.simulate_patch(todo_url, json={'name': 'new name'})
    assert result.status_code == 200
    assert result.json['name'] == 'new name'

    # testing delete
    result = falcon_client.simulate_delete(todo_url)
    assert result.status_code == 200
