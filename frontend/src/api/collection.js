import baseApi from './base';

const resource = 'collections/'

const createCollection = (data) => {
    return baseApi.post(resource, data)
}

const fetchCollections = (params) => {
    return baseApi.get(resource, { params })
}

const deleteCollection = (id) => {
    return baseApi.delete(`${resource}${id}/`)
}

export {
    createCollection,
    fetchCollections,
    deleteCollection
}
