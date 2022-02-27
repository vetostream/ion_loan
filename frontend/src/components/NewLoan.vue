<template>
    <div class="container is-fluid">
        <h1 class="has-text-left header">New Loan Request</h1>
        <div class="columns">
            <div class="column is-12">
                <b-field label="Client" :label-position="labelPosition">
                    <b-autocomplete
                        :data="clients"
                        :loading="isFetching"
                        placeholder="Search using Last Name"
                        icon="search"
                        field="pretty_result"
                        @input="getAsyncData"
                        @select="option => (selectedClient = option)">
                        <template #empty>No results found</template>
                    </b-autocomplete>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-6">
                <b-field label="Principal Amount" :label-position="labelPosition">
                    <b-input v-model="new_loan.principal_amount" v-cleave="masks.moneyField"></b-input>
                </b-field>
            </div>
            <div class="column is-6">
                <b-field label="Term in Months" :label-position="labelPosition">
                    <b-input v-model="new_loan.term" v-cleave="masks.numerical"></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-6">
                <b-field label="Interest (%)" :label-position="labelPosition">
                    <b-input v-model="new_loan.interest" v-cleave="masks.percentField"></b-input>
                </b-field>
            </div>
            <div class="column is-6">
                <b-field label="Loan Type" :label-position="labelPosition">
                    <b-select placeholder="Select a loan type" expanded v-model="new_loan.loan_type">
                        <option
                            v-for="option in loan_types"
                            :value="option.value"
                            :key="option.value">
                            {{ option.display }}
                        </option>
                    </b-select>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-6">
                <b-field label="Payment Start Date" :label-position="labelPosition">
                    <b-input v-model="new_loan.start_payment" v-cleave="masks.dateField" placeholder="MM/DD/YYYY"></b-input>
                </b-field>
            </div>
            <div class="column is-6">
                <b-field label="Control Number" :label-position="labelPosition">
                    <b-input v-model="new_loan.control_number"></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-6">
                <b-checkbox v-model="new_loan.is_advance">Advanced</b-checkbox>
            </div>
        </div>
        <b-button icon-left="check" type="is-success" expanded @click="requestLoan()">Request</b-button>
    </div>
</template>

<script>
import { searchClients } from '@/api/client.js'
import { createLoan } from '@/api/loan.js'
import debounce from 'lodash/debounce'

import Cleave from 'cleave.js'

import moment from 'moment';

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
    name: 'NewLoan',
    directives: {
        cleave
    },
    data() {
        return {
            labelPosition: 'inside',
            isLoading: false,
            selectedClient: null,
            isFetching: false,
            clients: [],
            new_loan: {
                client: null,
                term: '',
                interest: '',
                principal_amount: '',
                loan_type: '',
                is_advance: false,
                start_payment: ''
            },
            loan_types: [
                {value: 'pension', display: 'Pension'},
                {value: 'salary', display: 'Salary'},
            ],
            masks: {
                dateField: {
                    date: true,
                    datePattern: ['m','d','Y']
                },
                moneyField: {
                    numeral: true,
                    numeralDecimalScale: 2,
                    delimiter: '',
                    numeralPositiveOnly: true
                },
                percentField: {
                    numeral: true,
                    numeralDecimalScale: 2,
                    numeralPositiveOnly: true,
                    delimiter: ''
                },
                numerical: {
                    numeral: true,
                    numeralPositiveOnly: true,
                    delimiter: ''
                },
            }
        }
    },
    methods: {
        getAsyncData: debounce(function (lastname) {
            if (!lastname.length) {
                this.clients = []
                return
            }
            this.isFetching = true
            searchClients(lastname)
                .then(({ data }) => {
                    this.clients = []
                    this.clients = data.map(element => {
                        return {
                            ...element,
                            pretty_result: `${element.last_name}, ${element.first_name} (${element.birth_date})`
                        }
                    })
                })
                .catch((error) => {
                    this.clients = []
                    throw error
                })
                .finally(() => {
                    this.isFetching = false
                })
        }, 500),

        async requestLoan () {
            try {
                this.isLoading = true

                // transform date and amount
                const new_loan = {...this.new_loan}
                new_loan.start_payment = moment(new_loan.start_payment).format("YYYY-MM-DD")
                new_loan.maturity_date = moment(new_loan.start_payment).add(new_loan.term - 1, "months").format("YYYY-MM-DD")
                new_loan.principal_amount = parseFloat(new_loan.principal_amount.replace(/,/g, ''))

                await createLoan({
                    ...new_loan,
                    client: this.selectedClient.id
                })
                this.isLoading = false
                this.new_loan = {}
                this.selectedClient = null
                this.$buefy.toast.open({
                    message: 'Loan Request Saved Successfully.',
                    type: 'is-success'
                })
            } catch (err) {
                this.$buefy.toast.open({
                    message: `Something went wrong: ${err.message}`,
                    type: 'is-danger'
                })
            }
        }
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
</style>