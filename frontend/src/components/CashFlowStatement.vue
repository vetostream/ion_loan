<template>
    <div class="container-fluid">
        <h1 class="is-size-4 has-text-centered">
            {{ reportTitle }}
        </h1>
        <p class="is-size-6 has-text-centered" v-if="type === 'daily'">
            <i>{{ headerDate | humanDate }}</i>
        </p>
        <p class="is-size-6 has-text-centered" v-else>
            <i>{{ rangedDate }}</i>
        </p>
        <div class="columns" v-if="type === 'daily'">
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
                    <p class="control">
                        <b-button class="button is-info" icon-left="print" @click="printReport()">
                            Print
                        </b-button>
                    </p>
                </b-field>
            </div>
        </div>
        <div class="columns" v-else>
            <div class="column is-6">
                <b-field label="By Start Date to End Date" grouped>
                    <b-input v-cleave="masks.dateField" placeholder="mm/dd/yyyy" v-model="startDate" id="start-date" maxlength="10"></b-input>
                    <b-input v-cleave="masks.dateField" placeholder="mm/dd/yyyy" v-model="endDate" id="end-date" maxlength="10"></b-input>
                    <p class="control">
                        <b-button class="button is-success" icon-left="arrow-right" @click="fetchTransactionsByRange()">
                            Filter
                        </b-button>
                    </p>
                    <p class="control">
                        <b-button class="button is-info" icon-left="print" @click="printReport()">
                            Print
                        </b-button>
                    </p>
                </b-field>
            </div>
        </div>
        <div class="columns m-0 pb-0">
            <div class="column is-6 pb-0">
                <p class="is-size-4">BEGINNING BALANCE</p>
            </div>
            <div class="column is-6 pb-0">
                <p class="is-size-4 has-text-right">{{ openingCash.opening_balance | displayMoney }}</p>
            </div>
        </div>
        <b-table :data="dailyTransactions" :columns="type === 'daily' ? columns : rangedColumns" class="m-0 p-0" :loading="isLoading">
            <template #footer>
                <th>
                    <div class="th-wrap">
                        <h1 class="is-size-4">TOTAL</h1>
                    </div>
                </th>
                <th v-if="type !== 'daily'"></th>
                <th>
                    <h1 class="is-size-4 has-text-success has-text-right">{{ debitTotal | displayMoney }}</h1>
                </th>
                <th>
                    <h1 class="is-size-4 has-text-danger has-text-right">{{ creditTotal | displayMoney }}</h1>
                </th>
            </template>
            <template #empty>
                <div class="has-text-centered">
                    <p class="is-size-5">No Transactions</p>
                </div>
            </template>
        </b-table>
        <div class="columns m-0 pb-0">
            <div class="column is-6 pb-0">
                <p class="is-size-4">ENDING BALANCE</p>
            </div>
            <div class="column is-6 pb-0">
                <p class="is-size-4 has-text-right">{{ endingBalance | displayMoney }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import { fetchTransactionsByDate, fetchRangedTransactions, calculateOpeningCash } from '@/api/transaction.js'
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
    props: {
        initialType: String
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
            openingCash: {
                opening_balance: 0
            },
            columns: [
                {
                    field: 'description',
                    label: 'Transaction Description',
                },
                {
                    field: 'debit_amount',
                    label: 'DEBIT',
                    numeric: true,
                },
                {
                    field: 'credit_amount',
                    label: 'CREDIT',
                    numeric: true,
                }
            ],
            rangedColumns: [
                {
                    field: 'post_date_human',
                    label: 'Post Date'
                },
                {
                    field: 'description',
                    label: 'Transaction Description',
                },
                {
                    field: 'debit_amount',
                    label: 'DEBIT',
                    numeric: true,
                },
                {
                    field: 'credit_amount',
                    label: 'CREDIT',
                    numeric: true,
                }
            ],
            filterDate: null,
            masks: {
                dateField: {
                    date: true,
                    datePattern: ['m', 'd', 'Y'],
                }
            },
            type: this.initialType,
            rangedDate: '',
            startDate: null,
            endDate: null,
            isLoading: false
        }
    },
    async created() {
        if (this.type === 'daily') {
            this.fetchTransactions()
        }
    },
    mounted() {
        if (this.type === 'daily') {
            document.getElementById('filter-date').addEventListener('keydown', function(e) {
                if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                    e.preventDefault();
                }
            });
        } else {
            document.getElementById('start-date').addEventListener('keydown', function(e) {
                if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                    e.preventDefault();
                }
            });
            document.getElementById('end-date').addEventListener('keydown', function(e) {
                if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                    e.preventDefault();
                }
            });
        }
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
        },
        reportTitle () {
            if (this.type === 'ranged') {
                return "Cash Flow Statement"
            } else {
                return "Daily Cash Flow Statement"
            }
        },
        endingBalance () {
            if (!!this.debitTotal && !!this.creditTotal && !!this.openingCash) {
                if (this.openingCash.side === 'debit') {
                    return (parseFloat(this.openingCash.opening_balance) + this.debitTotal) - this.creditTotal
                } else {
                    return this.debitTotal - (this.creditTotal +  parseFloat(this.openingCash.opening_balance))
                }
            } else if (!!this.openingCash) {
                return this.openingCash.opening_balance
            }

            return 0
        }
    },
    watch: {
        initialType() {
            if (this.initialType === 'daily') {
                this.type = 'daily'
                this.fetchTransactions()
            } else {
                this.type = 'ranged'
                this.dailyTransactions = []
            }
        }
    },
    methods: {
        async fetchTransactions() {
            this.isLoading = true
            let transactions = null
            let openingCash = {}
            if (!this.filterDate) {
                const now = moment().format("YYYY-MM-DD")
                transactions = await fetchTransactionsByDate(now)
                openingCash = await calculateOpeningCash(moment().format('YYYY-MM-DD'))
            } else {
                transactions = await fetchTransactionsByDate(moment(this.filterDate).format("YYYY-MM-DD"))
                openingCash = await calculateOpeningCash(moment(this.filterDate).format('YYYY-MM-DD'))
            }

            this.openingCash = openingCash.data

            this.dailyTransactions = transactions.data.map((transaction) => {
                return {
                    ...transaction,
                    debit_amount: transaction.transaction_side === 'debit' ? `${toCurrency.format(transaction.amount)}` : '',
                    credit_amount: transaction.transaction_side === 'credit' ? `-${toCurrency.format(transaction.amount)}` : '',
                }
            });
            this.isLoading = false
            // this.dailyTransactions = [{
            //     description: 'BEGINNING BALANCE',
            //     debit_amount: this.openingCash.side === 'debit' ? `${toCurrency.format(this.openingCash.opening_balance)}` : '',
            //     credit_amount: this.openingCash.side === 'credit' ? `${toCurrency.format(this.openingCash.opening_balance)}` : ''
            // }].concat(dailyTransactions)
        },
        async fetchTransactionsByRange() {
            this.isLoading = true
            const startDate = moment(this.startDate).format("YYYY-MM-DD")
            const endDate = moment(this.endDate).format("YYYY-MM-DD")

            const openingCash = await calculateOpeningCash(startDate)
            this.rangedDate = `${moment(startDate).format("MMMM Do, YYYY")} to ${moment(endDate).format("MMMM Do, YYYY")}`

            const transactions = await fetchRangedTransactions({
                start_date: startDate,
                end_date: endDate
            })
            this.openingCash = openingCash.data
            this.dailyTransactions = transactions.data.map((transaction) => {
                    return {
                        post_date_human: moment(transaction.post_date).format("MM/DD/YYYY"),
                        ...transaction,
                        debit_amount: transaction.transaction_side === 'debit' ? `${toCurrency.format(transaction.amount)}` : '',
                        credit_amount: transaction.transaction_side === 'credit' ? `-${toCurrency.format(transaction.amount)}` : '',
                    }
                });
            this.isLoading = false
        },
        resetToday() {
            this.filterDate = null
            this.fetchTransactions()
        },
        printReport() {
            if (this.type === 'ranged') {
                const startDate = moment(this.startDate).format("YYYY-MM-DD")
                const endDate = moment(this.endDate).format("YYYY-MM-DD")
                window.open(`${process.env.VUE_APP_API_ENDPOINT_URL}reports/cash_flow_statement/${startDate}/${endDate}/`)
            } else {
                let startDate = moment().format("YYYY-MM-DD")
                if (this.filterDate) {
                    startDate = moment(this.filterDate).format("YYYY-MM-DD")
                }

                window.open(`${process.env.VUE_APP_API_ENDPOINT_URL}reports/cash_flow_statement/${startDate}/`)
            }
        }
    }
}
</script>

<style>
    small.counter {
        display: none !important;
    }
</style>