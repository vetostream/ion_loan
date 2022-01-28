<template>
    <div class="container is-fluid">
        <div class="columns">
            <div class="column is-4">
                <label for="">Client</label>
                <h3>{{ loanDetail.full_name }}</h3>
            </div>
            <div class="column is-4">
                <label for="">Date of Birth</label>
                <h3>{{ loanDetail.birth_date }}</h3>
            </div>
            <div class="column is-4">
                <label for="">Principal Amount</label>
                <h3>{{ loanDetail.principal_amount | displayMoney }}</h3>
            </div>
        </div>
        <div class="columns">
            <div class="column is-4">
                <label for="">Term in Months</label>
                <h3>{{ loanDetail.term }}</h3>
            </div>
            <div class="column is-4">
                <label for="">Interest</label>
                <h3>{{ loanDetail.interest }}</h3>
            </div>
            <div class="column is-4">
                <label for="">Loan Type</label>
                <h3>{{ loanDetail.loan_type }}</h3>
            </div>
        </div>
        <div class="columns">
            <div class="column is-4">
                <label for="">Start Payment Date</label>
                <h3>{{ loanDetail.start_payment | shortDate }}</h3>
            </div>
            <div class="column is-4">
                <label for="">Maturity Date</label>
                <h3>{{ maturityDate | shortDate }}</h3>
            </div>
            <div class="column is-4">
                <b-checkbox v-model="loanDetail.is_advanced" disabled>Advanced</b-checkbox>
            </div>
        </div>
        <hr>
        <div class="columns">
            <div class="column is-4">
                <label for="">Principal Amount</label>
            </div>
            <div class="column is-4">
                <p>-------------------------------------</p>
            </div>
            <div class="column is-4">
                {{ loanDetail.principal_amount | displayMoney }}
            </div>
        </div>
        <div class="columns">
            <div class="column is-4">
                <label for="">U.D.I</label>
            </div>
            <div class="column is-4">
                <p>-------------------------------------</p>
            </div>
            <div class="column is-4">
                ( {{ calculatedUDI | displayMoney }} )
            </div>
        </div>
        <div class="columns">
            <div class="column is-4">
                <label for="">Total Amount of Loan</label>
            </div>
            <div class="column is-4">
                <p>-------------------------------------</p>
            </div>
            <div class="column is-4">
                {{ totalLoanAmount | displayMoney }}
            </div>
        </div>
        <div class="columns">
            <div class="column is-4">
                <label for="">Gross Cash Out</label>
            </div>
            <div class="column is-4">
                <p>-------------------------------------</p>
            </div>
            <div class="column is-4">
                {{ grossCashOut | displayMoney }}
            </div>
        </div>
        <div class="columns">
            <div class="column is-12">
                <label for="">LESS Fees:</label>
            </div>
        </div>
        <div class="columns">
            <div class="column is-4">
                <!-- <label class="has-text-right" for="">L.L.R.F</label> -->
            </div>
            <div class="column is-4">
                <label class="has-text-right" for="">L.L.R.F</label>
            </div>
            <div class="column is-4">
                ( {{ calculatedLLRF | displayMoney }} )
            </div>
        </div>
        <div class="columns">
            <div class="column is-4">
                <!-- <label for="">Processing Fee</label> -->
            </div>
            <div class="column is-4">
                <label for="">Processing Fee</label>
            </div>
            <div class="column is-4">
                ( {{ processFee | displayMoney }} )
            </div>
        </div>
        <div class="columns" v-if="feeOthers">
            <div class="column is-4">
                <!-- <label for="">Processing Fee</label> -->
            </div>
            <div class="column is-4">
                <label for="">Others</label>
            </div>
            <div class="column is-4">
                ( {{ feeOthers | displayMoney }} )
            </div>
        </div>
        <div class="columns">
            <div class="column is-4">
                <label for="">Total Deductions</label>
            </div>
            <div class="column is-4">
                <p>-------------------------------------</p>
            </div>
            <div class="column is-4">
                ( {{ calculatedLLRF + processFee + calculatedUDI + feeOthers | displayMoney }} )
            </div>
        </div>
        <div class="columns">
            <div class="column is-4">
                <label for="">Net Cash Out</label>
            </div>
            <div class="column is-4">
                <p>-------------------------------------</p>
            </div>
            <div class="column is-4">
                {{ netCashout | displayMoney }}
            </div>
        </div>
        <b-table :data="payment_schedule" :columns="columns" v-if="payment_schedule.length > 0" />
        <br>
        <div class="columns" v-if="!is_approved">
            <div class="column is-6">
                <b-button icon-left="check" type="is-success" expanded @click="approveLoan()">Approve</b-button>
            </div>
            <div class="column is-6">
                <b-button icon-left="times-circle" type="is-danger" expanded @click="requestLoan()">Decline</b-button>
            </div>
        </div>
    </div>
</template>

<script>
import { approveLoan } from '@/api/loan.js'
import moment from 'moment';

const toCurrency = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'PHP'
})

export default {
    name: 'LoanDetail',
    props: {
        selected_loan: Object,
        is_approved: {
            type: Boolean,
            default: false
        }
    },
    filters: {
        displayMoney(value) {
            return toCurrency.format(value)
        },
        shortDate(value) {
            return moment(value).format("MM/DD/YYYY")
        }
    },
    data() {
        return {
            labelPosition: 'inside',
            isLoading: false,
            loan_types: [
                {value: 'pension', display: 'Pension'},
                {value: 'salary', display: 'Salary'},
            ],
            payment_schedule: [],
            columns: [
                {
                    field: 'payment_date',
                    label: 'Payment Date'
                },
                {
                    field: 'amount',
                    label: 'Amount',
                    centered: true
                },
                {
                    field: 'running_balance',
                    label: 'Running Balance',
                    centered: true
                }
            ],
            processFee: 150,
        }
    },
    created() {
        this.generatePaymentSchedule()
    },
    computed: {
        loanDetail() {
            return this.selected_loan || {
                client: null,
                term: '',
                interest: '',
                principal_amount: '',
                loan_type: '',
                is_advance: false,
                start_payment: '',
                full_name: '',
                birth_date: '',
                fee_others: 0,
            }
        },
        feeOthers() {
            const fee = parseFloat(this.loanDetail.fee_others)
            if (fee) {
                return fee
            }

            return 0
        },
        netCashout() {
            const parsedAmount = parseFloat(this.loanDetail.principal_amount)
            return parsedAmount - this.totalDeductions
        },
        totalLoanAmount() {
            const parsedAmount = parseFloat(this.loanDetail.principal_amount)

            return parsedAmount + this.calculatedUDI
        },
        grossCashOut() {
            const parsedAmount = parseFloat(this.loanDetail.principal_amount)

            return parsedAmount - this.calculatedUDI
        },
        calculatedUDI() {
            const interestRate = parseFloat(this.loanDetail.interest / 100)
            const parsedAmount = parseFloat(this.loanDetail.principal_amount)
            const parsedTerm = parseInt(this.loanDetail.term)
            return parsedAmount * interestRate * parsedTerm
        },
        calculatedLLRF() {
            return (parseFloat(this.loanDetail.principal_amount) / 1000) * (parseInt(this.loanDetail.term) + 1)
        },
        maturityDate() {
            const startPaymentDate = moment(this.loanDetail.start_payment)
            const calculated_term = parseInt(this.loanDetail.term)
            return startPaymentDate.add(calculated_term - 1, "months")
        },
        totalDeductions() {
            return this.calculatedLLRF + this.processFee + this.calculatedUDI + this.feeOthers
        }
    },
    methods: {
        generatePaymentSchedule() {
            // this method generate a payment schedule on real time
            // so that the user can have an idea what the payment schedule looks like
            const startPaymentDate = moment(this.loanDetail.start_payment)
            const calculated_term = parseInt(this.loanDetail.term)
            const cycles = Array.from(Array(calculated_term).keys())
            const amount = parseFloat(this.loanDetail.principal_amount) / calculated_term

            let dateCounter = null;

            this.payment_schedule = cycles.map((cycle) => {
                const running_balance = (this.loanDetail.principal_amount) - (amount * (cycle + 1))
                if (cycle === 0) {
                    return {
                        payment_date: startPaymentDate.format('MM/DD/YYYY'),
                        amount: toCurrency.format(amount),
                        running_balance: toCurrency.format(running_balance)
                    }
                } else {
                    // dateCounter = startPaymentDate.add(15, "days")
                    dateCounter = startPaymentDate.add(1, "months")
                    return {
                        payment_date: dateCounter.format('MM/DD/YYYY'),
                        amount: toCurrency.format(amount),
                        running_balance: toCurrency.format(running_balance)
                    }
                }
            });
        },
        async approveLoan() {
            try {
                const response = await approveLoan(this.loanDetail.id, {
                    net_cash_out: parseFloat(this.netCashout)
                })
                this.$buefy.toast.open({
                    message: 'Loan Approved!',
                    type: 'is-success'
                })
                this.is_approved = true
            } catch (err) {
                this.$buefy.toast.open({
                    message: `Something went wrong: ${err.message}`,
                    type: 'is-danger'
                })
            }
        },
    }
}
</script>

<style>
    .header {
        margin-bottom: 1.5em;
    }

    .columns {
        text-align: left;
    }

    label {
        font-weight: bold;
    }
</style>
