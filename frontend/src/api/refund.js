import baseApi from './base';

const resource = 'refunds/'

const createRefund = (data) => {
    return baseApi.post(resource, data)
}

export {
    createRefund,
}
