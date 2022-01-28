import baseApi from './base';

const resource = 'collections/'

const createCollection = (data) => {
    return baseApi.post(resource, data)
}

const fetchCollections = (data) => {
    return baseApi.get(resource, data)
}

export {
    createCollection,
    fetchCollections
}
