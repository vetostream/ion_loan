<template>
    <div class="container is-fluid">
        <h1 class="has-text-left header">Creating an Expense</h1>
        <div class="columns">
            <div class="column is-6">
                <b-field label="Post Date" :label-position="labelPosition">
                    <b-input v-model="post_date" v-cleave="masks.dateField" placeholder="mm/dd/yyyy"></b-input>
                </b-field>
            </div>
            <div class="column is-6">
                <b-field label="Expense Amount" :label-position="labelPosition">
                    <b-input v-model="amount" v-cleave="masks.moneyField"></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-12">
                <b-field label="Description" :label-position="labelPosition">
                    <b-input v-model="description" maxlength="200" type="textarea"></b-input>
                </b-field>
            </div>
        </div>
        <b-button icon-left="check" type="is-success" expanded @click="submitExpense()">Submit</b-button>
    </div>
</template>

<script>
import { createExpense } from '@/api/transaction.js'
import Cleave from 'cleave.js'
import moment from 'moment'

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
    name: 'CreateExpense',
    directives: {
        cleave
    },
    data() {
        return {
            labelPosition: 'inside',
            isLoading: false,
            post_date: '',
            amount: '',
            description: '',
            masks: {
                dateField: {
                    date: true,
                    datePattern: ['m','d','Y']
                },
                moneyField: {
                    numeral: true,
                    numeralDecimalScale: 2,
                    numeralPositiveOnly: true
                },
            }
        }
    },
    methods: {
        async submitExpense() {
            try {
                this.isLoading = true

                // transform date and amount
                this.amount = parseFloat(this.amount.replace(/,/g, ''))

                const data = {
                    amount: this.amount,
                    description: `(EXPENSE) ${this.description}`,
                    post_date: moment(this.post_date).format("YYYY-MM-DD"),
                    transaction_side: 'credit',
                    account: 'liabilities'
                }

                const response = await createExpense(data)

                this.amount = ''
                this.description = ''
                this.post_date = ''

                this.$buefy.toast.open({
                    message: `Expense Successfully Posted!`,
                    type: 'is-warning'
                })

            } catch (err) {
                this.$buefy.toast.open({
                    message: `Something went wrong: ${err.message}`,
                    type: 'is-danger'
                })
            }

            this.isLoading = false
        }
    }
}
</script>

<style>
    .header {
        margin-bottom: 1.5em;
    }
</style>