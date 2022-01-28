<template>
    <div class="container-fluid">
        <h1 class="is-size-4 has-text-centered">Daily Cash Flow Statement</h1>
        <p class="is-size-6 has-text-centered">
            <i>{{ headerDate | humanDate }}</i>
        </p>
        <div class="columns">
            <div class="column is-3">
                <b-field label="Filter by Date" grouped>
                    <b-input v-cleave="masks.dateField" placeholder="mm/dd/yyyy" v-model="filterDate" id="filter-date" maxlength="10"></b-input>
                    <p class="control">
                        <b-button class="button is-success" icon-left="arrow-right" @click="fetchTransactions()">
                            Filter
                        </b-button>
                    </p>
                    <p class="control">
                        <b-button class="button is-info" icon-left="undo" @click="resetToday()">
                            Today
                        </b-button>
                    </p>
                </b-field>
            </div>
        </div>
        <b-table :data="dailyTransactions" :columns="columns">
            <template #footer>
                <th>
                    <div class="th-wrap">
                        <h1 class="is-size-4">TOTAL</h1>
                    </div>
                </th>
                <th>
                    <h1 class="is-size-4">{{ debitTotal | displayMoney }}</h1>
                </th>
                <th>
                    <h1 class="is-size-4">{{ creditTotal | displayMoney }}</h1>
                </th>
            </template>
            <template #empty>
                <div class="has-text-centered">
                    <p class="is-size-5">No Transactions</p>
                </div>
            </template>
        </b-table>
    </div>
</template>

<script>
import { fetchTransactionsByDate } from '@/api/transaction.js'
import moment from 'moment'
import Cleave from 'cleave.js'

const toCurrency = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'PHP'
})

const cleave = {
    name: 'cleave',
    bind(el, binding) {
        const input = el.querySelector('input')
        input._vCleave = new Cleave(input, binding.value)
    },
    unbind(el) {
        const input = el.querySelector('input')
        input._vCleave.destroy()
    }
}

export default {
    name: 'CashFlowStatement',
    directives: {
        cleave
    },
    filters: {
        displayMoney(value) {
            return toCurrency.format(value)
        },
        humanDate(value) {
            return moment(value).format("MMMM Do, YYYY")
        }
    },
    data() {
        return {
            dailyTransactions: [],
            columns: [
                {
                    field: 'description',
                    label: 'Transaction Description',
                },
                {
                    field: 'debit_amount',
                    label: 'DEBIT',
                },
                {
                    field: 'credit_amount',
                    label: 'CREDIT',
                }
            ],
            filterDate: null,
            masks: {
                dateField: {
                    date: true,
                    datePattern: ['m', 'd', 'Y'],
                }
            },
        }
    },
    async created() {
        this.fetchTransactions()
    },
    mounted() {
        document.getElementById('filter-date').addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                e.preventDefault();
            }
        });
    },
    computed: {
        debitTotal() {
            const transactions = [...this.dailyTransactions]
            return transactions.reduce((partial_sum, a) => {
                if (a.transaction_side === 'debit') {
                    return partial_sum + parseFloat(a.amount)
                } else {
                    return partial_sum + 0
                }
            }, 0);
        },
        creditTotal() {
            const transactions = [...this.dailyTransactions]
            return transactions.reduce((partial_sum, a) => {
                if (a.transaction_side === 'credit') {
                    return partial_sum + parseFloat(a.amount)
                } else {
                    return partial_sum + 0
                }
            }, 0);
        },
        headerDate() {
            if (this.filterDate) {
                return this.filterDate
            }

            return moment().format("YYYY-MM-DD")
        }
    },
    methods: {
        async fetchTransactions() {
            let transactions = null
            if (!this.filterDate) {
                const now = moment().format("YYYY-MM-DD")
                transactions = await fetchTransactionsByDate(now)
            } else {
                transactions = await fetchTransactionsByDate(moment(this.filterDate).format("YYYY-MM-DD"))
            }

            this.dailyTransactions = transactions.data.map((transaction) => {
                return {
                    ...transaction,
                    debit_amount: transaction.transaction_side === 'debit' ? `${toCurrency.format(transaction.amount)}` : '',
                    credit_amount: transaction.transaction_side === 'credit' ? `-${toCurrency.format(transaction.amount)}` : '',
                }
            });
        },
        resetToday() {
            this.filterDate = null
            this.fetchTransactions()

            
        }
    }
}
</script>

<style>
    small.counter {
        display: none !important;
    }
</style>