import baseApi from './base';

const resource = 'collections/'

const createCollection = (data) => {
    return baseApi.post(resource, data)
}

const fetchCollections = (params) => {
    return baseApi.get(resource, { params })
}

export {
    createCollection,
    fetchCollections
}
