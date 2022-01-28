import baseApi from './base';

const resource = 'transactions/'

const fetchTransactionsByDate = (transaction_date) => {
    return baseApi.get(resource, { params: {transaction_date} })
}

export {
    fetchTransactionsByDate
}
