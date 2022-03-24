import baseApi from './base';

const resource = 'transactions/'
const subroutes = 'functions/'

const fetchTransactionsByDate = (transaction_date) => {
    return baseApi.get(resource, { params: {transaction_date} })
}

const fetchRangedTransactions = (data) => {
    return baseApi.get(resource, {params: data})
}

const createExpense = (data) => {
    return baseApi.post(resource, data)
}

const createEntry = (data) => {
    return baseApi.post(resource, data)
}

const calculateOpeningCash = (startDate) => {
    return baseApi.get(`${subroutes}calculate_opening_cash/${startDate}`)
}

export {
    fetchTransactionsByDate,
    fetchRangedTransactions,
    createExpense,
    createEntry,
    calculateOpeningCash
}
