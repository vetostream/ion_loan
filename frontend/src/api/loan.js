import baseApi from './base';

const resource = 'loans/'

const createLoan = (data) => {
    return baseApi.post(resource, data)
}

const getLoan = (id) => {
    return baseApi.get(`${resource}/${id}`)
}

const approveLoan = (id, data) => {
    return baseApi.post(`${resource}${id}/approve_loan/`, { ...data, loan_status: 'approved' })
}

const deleteLoan = (id) => {
    return baseApi.delete(`${resource}${id}/`)
}

const searchLoans = (params) => {
    return baseApi.get(`${resource}`, { params })
}

export {
    createLoan,
    getLoan,
    searchLoans,
    approveLoan,
    deleteLoan
}
