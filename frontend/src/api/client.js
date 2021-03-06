import baseApi from './base';

const resource = 'clients/'

const createClient = (data) => {
    return baseApi.post(resource, data)
}

const getClient = (id) => {
    return baseApi.get(`${resource}${id}`)
}

const searchClients = (lastname) => {
    return baseApi.get(`${resource}`, {
        params: {
            lastname: lastname
        }
    })
}

export {
    createClient,
    getClient,
    searchClients
}
