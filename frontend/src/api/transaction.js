import baseApi from './base';

const resource = 'transactions/'

const fetchTransactionsByDate = (transaction_date) => {
    return baseApi.get(resource, { params: {transaction_date} })
}

const fetchRangedTransactions = (data) => {
    return baseApi.get(resource, {params: data})
}

const createExpense = (data) => {
    return baseApi.post(resource, data)
}

export {
    fetchTransactionsByDate,
    fetchRangedTransactions,
    createExpense
}
