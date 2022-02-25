<template>
    <div class="container is-fluid">
        <h1 class="has-text-left header">Creating a New Client</h1>
        <div class="columns">
            <div class="column is-4">
                <b-field label="First Name" :label-position="labelPosition">
                    <b-input v-model="client.first_name"></b-input>
                </b-field>
            </div>
            <div class="column is-4">
                <b-field label="Middle Name" :label-position="labelPosition">
                    <b-input v-model="client.middle_name"></b-input>
                </b-field>
            </div>
            <div class="column is-4">
                <b-field label="Last Name" :label-position="labelPosition">
                    <b-input v-model="client.last_name"></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-12">
                <b-field label="Address" :label-position="labelPosition">
                    <b-input v-model="client.address"></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-6">
                <b-field label="Contact No" :label-position="labelPosition">
                    <b-input v-model="client.contact_number"></b-input>
                </b-field>
            </div>
            <div class="column is-6">
                <b-field label="Date of Birth" :label-position="labelPosition">
                    <b-input v-model="client.birth_date" v-cleave="masks.dateField" placeholder="MM/DD/YYYY"></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-6">
                <b-field label="Bank Name" :label-position="labelPosition">
                    <b-input v-model="client.bank_name"></b-input>
                </b-field>
            </div>
            <div class="column is-6">
                <b-field label="Account Number" :label-position="labelPosition">
                    <b-input v-model="client.account_number"></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-6">
                <b-field label="Pension Amount" :label-position="labelPosition">
                    <b-input v-model="client.pension" v-cleave="masks.moneyField"></b-input>
                </b-field>
            </div>
            <div class="column is-6">
                <b-field label="SSS Number" :label-position="labelPosition">
                    <b-input v-model="client.sss_no"></b-input>
                </b-field>
            </div>
        </div>
        <div class="columns">
            <div class="column is-12">
                <b-field label="Co-Maker Full Name" :label-position="labelPosition">
                    <b-input v-model="client.co_maker"></b-input>
                </b-field>
            </div>
        </div>
        <b-button icon-left="check" type="is-success" expanded @click="submitClient()">Submit</b-button>
    </div>
</template>

<script>
import { createClient } from '@/api/client.js'
import Cleave from 'cleave.js'

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
    name: 'NewClient',
    directives: {
        cleave
    },
    data() {
        return {
            labelPosition: 'inside',
            client: {
                first_name: '',
                last_name: '',
                middle_name: '',
                address: '',
                contact_number: '',
                birth_date: '',
                pension: '',
                sss_no: '',
                co_maker: ''
            },
            isLoading: false,
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
        async submitClient() {
            try {
                this.isLoading = true

                // transform date and amount
                const client = {...this.client}

                client.pension = parseFloat(this.client.pension.replace(/,/g, ''))

                const response = await createClient(client)

                this.$buefy.toast.open({
                    message: `Client Successfully Created!`,
                    type: 'is-success'
                })

                this.client = {}
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