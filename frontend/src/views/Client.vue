<template>
    <div class="container is-fluid">
        <b-tabs type="is-boxed" expanded>
            <b-tab-item label="Client" icon="user">
                <div class="tab-container">
                    <div v-if="readMode">
                        <div class="columns">
                            <div class="column is-4">
                                <label for="">First Name</label>
                                <p>{{ client.first_name }}</p>
                            </div>
                            <div class="column is-4">
                                <label for="">Middle Name</label>
                                <p>{{ client.middle_name }}</p>
                            </div>
                            <div class="column is-4">
                                <label for="">Last Name</label>
                                <p>{{ client.last_name }}</p>
                            </div>
                        </div>
                        <hr>
                        <div class="columns">
                            <div class="column is-12">
                                <label for="">Address</label>
                                <p>{{ client.address }}</p>
                            </div>
                        </div>
                        <hr>
                        <div class="columns">
                            <div class="column is-6">
                                <label for="">Contact No</label>
                                <p>{{ client.contact_number }}</p>
                            </div>
                            <div class="column is-6">
                                <label for="">Date of Birth</label>
                                <p>{{ client.birth_date }}</p>
                            </div>
                        </div>
                        <hr>
                        <div class="columns">
                            <div class="column is-6">
                                <label for="">Pension Amount</label>
                                <p>{{ client.pension }}</p>
                            </div>
                            <div class="column is-6">
                                <label for="">SSS Number</label>
                                <p>{{ client.sss_no }}</p>
                            </div>
                        </div>
                        <hr>
                        <div class="columns">
                            <div class="column is-6">
                                <label for="">Bank Name</label>
                                <p>{{ client.bank_name }}</p>
                            </div>
                            <div class="column is-6">
                                <label for="">Account Number</label>
                                <p>{{ client.account_number }}</p>
                            </div>
                        </div>            
                        <hr>
                        <div class="columns">
                            <div class="column is-12">
                                <label for="">Co-Maker Full Name</label>
                                <p>{{ client.co_maker }}</p>
                            </div>
                        </div>
                    </div>
                    <div v-else>
                        <h1 class="has-text-left header">Edit Client</h1>
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
                    </div>
                </div>
            </b-tab-item>
            <b-tab-item label="Loans" icon="coins">
                <div class="tab-container">
                    <div class="columns">
                        <div class="column is-12">
                            <b-button class="button is-success" icon-left="money-check" @click="paymentModalActive=true">Post Payment</b-button>
                        </div>
                    </div>
                    <div class="columns" v-if="selectedRows.length > 0">
                        <div class="column is-4">
                            <b-field label="Reference" :label-position="labelPosition">
                                <b-input v-model="collection.reference_code"></b-input>
                            </b-field>
                        </div>
                        <div class="column is-4">
                            <b-field label="Amount" :label-position="labelPosition">
                                <b-input v-model="collection.amount" v-cleave="masks.moneyField"></b-input>
                            </b-field>
                        </div>
                        <div class="column is-4">
                            <b-button
                                label="Create Collection"
                                type="is-info"
                                size="is-medium"
                                :disabled="!canCreateCollection"
                                @click="confirmCreateCollection" />
                        </div>
                    </div>
                    <div class="columns">
                        <div class="column is-12">
                            <b-table :data="loans" :columns="columns" :loading="isLoading" checkable :checked-rows.sync="selectedRows"
                                :row-class="(row) => row.is_collected && 'is-success'"
                                :header-checkable="false"
                                :is-row-checkable="(row) => !row.is_collected">
                                <template #empty>
                                    <div class="has-text-centered">No Results Found</div>
                                </template>
                            </b-table>
                        </div>
                    </div>
                    <!--
                    <hr>
                    <h1 class="is-size-4 has-text-left table-title">Collections</h1>
                    <div class="columns">
                        <div class="column is-12">
                            <b-table :data="collections" :columns="collectionColumns" :loading="isLoading" checkable :checked-rows.sync="selectedCollections"
                                :header-checkable="false"
                                detailed
                                detail-key="id"
                                >
                                <b-table-column field="date_created_short" label="Date Created" v-slot="props">
                                    <a @click="props.toggleDetails(props.row)">
                                        {{ props.row.date_created_short }}
                                    </a>
                                </b-table-column>
                                <template #empty>
                                    <div class="has-text-centered">No Results Found</div>
                                </template>

                                <template #detail="props">
                                    <div class="columns" v-for="detail in props.row.collection_details" :key="detail.id">
                                        <div class="column is-12 collection-detail">
                                            <p>{{ detail.paid_transaction_id }} | Amount: {{ detail.amount_used }}</p>
                                        </div>
                                    </div>
                                </template>
                            </b-table>
                        </div>
                    </div>
                    -->
                </div>
            </b-tab-item>
        </b-tabs>

        <b-modal
            :active="paymentModalActive"
            has-modal-card
            trap-focus
            aria-role="dialog"
            aria-label="Post Payment"
            close-button-aria-label="Close"
            aria-modal>
            <div class="modal-card" style="width: auto">
                <header class="modal-card-head">
                    <p class="modal-card-title">Post Payment</p>
                </header>
                <section class="modal-card-body">
                    <div class="columns">
                        <div class="column is-12">
                            <b-field label="Post Date" :label-position="labelPosition">
                                <b-input v-model="collection.post_date" v-cleave="masks.dateField" placeholder="mm/dd/yyyy"></b-input>
                            </b-field>
                        </div>
                    </div>
                    <div class="columns">
                        <div class="column is-12">
                            <b-field label="Amount" :label-position="labelPosition">
                                <b-input v-model="collection.amount" v-cleave="masks.moneyField"></b-input>
                            </b-field>
                        </div>
                    </div>
                    <div class="columns">
                        <div class="column is-12">
                            <b-field label="Reference Code" :label-position="labelPosition">
                                <b-input v-model="collection.reference_code"></b-input>
                            </b-field>
                        </div>
                    </div>
                </section>
                <footer class="modal-card-foot">
                    <b-button
                        label="Cancel"
                        @click="paymentModalActive=false" />
                    <b-button
                        label="Post"
                        type="is-success"
                        @click="processPayment()" />
                </footer>
            </div>
        </b-modal>
    </div>
</template>

<script>
import Cleave from 'cleave.js'
import { getClient } from '@/api/client.js'
import { createCollection } from '@/api/collection.js'
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

const toCurrency = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'PHP'
})

export default {
    name: 'ClientDetail',
    directives: {
        cleave
    },
    filters: {
        shortDate(value) {
            return moment(value).format("MM/DD/YYYY")
        }
    },
    data() {
        return {
            labelPosition: 'inside',
            isLoading: false,
            readMode: true,
            client: {},
            loans: [],
            selectedRows: [],
            collection: {
                reference_code: '',
                amount: ''
            },
            paymentModalActive: false,
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
            },
            columns: [
                {
                    field: 'control_number',
                    label: 'Control Number'
                },
                {
                    field: 'humanized_date_payment',
                    label: 'Payment Due Date',
                },
                {
                    field: 'humanized_loan_amount',
                    label: 'Principal Amount',
                    centered: true
                },
                {
                    field: 'humanized_amount',
                    label: 'Amount',
                    centered: true
                },
                {
                    field: 'humanized_balance',
                    label: 'Running Balance',
                    centered: true
                },
                {
                    field: 'receivable',
                    label: 'AR'
                },
                {
                    field: 'payable',
                    label: 'AP'
                },
            ],
            selectedCollections: [],
            collectionColumns: [
                {
                    field: 'date_created_short',
                    label: 'Collection Date',
                },
                {
                    field: 'reference_code',
                    label: 'Reference Code',
                    centered: true
                },
                {
                    field: 'amount_used_string',
                    label: 'Collection Amount',
                    centered: true
                },
                {
                    field: 'refundable_string',
                    label: 'AP',
                    centered: true
                }
            ],
            collections: [],
        }
    },
    created() {
        this.isLoading = true
        this.fetchClients();
        this.isLoading = false
    },
    computed: {
        canCreateCollection() {
            if (this.collection.amount === '' || this.calculateAP() < 0) {
                return false
            }

            return true
        },        
    },
    methods: {
        async fetchClients() {
            const response = await getClient(this.$route.params.id)
            this.client = response.data
            this.loans = this.client.active_loans.map((loan) => {
                return {
                    ...loan,
                    id_display: `LOAN-${loan.loan}`,
                    is_paid: loan.is_paid ? 'Collected' : '',
                    is_collected: loan.is_paid,
                    humanized_date_payment: moment(loan.date_payment).format('MM/DD/YYYY'),
                    humanized_loan_amount: toCurrency.format(loan.loan_amount),
                    humanized_amount: toCurrency.format(loan.amount),
                    humanized_balance: toCurrency.format(loan.balance),
                    control_number: loan.loan_control_number
                }
            })
            this.collections = this.client.collections.map((collection) => {
                return {
                    ...collection,
                    date_created_short: moment(collection.date_created).format("MM/DD/YYYY"),
                    amount_used_string: toCurrency.format(collection.collection_amount),
                    refundable_string: toCurrency.format(collection.refundable_amount),
                }
            })
        },
        calculateAP() {
            const totalAmountToPay = this.selectedRows.reduce((partial_sum, a) => {
                return partial_sum + parseFloat(a.amount)
            }, 0);

            return parseFloat(this.collection.amount.replace(',', '')) - (totalAmountToPay)
        },
        generateCollectionMessage() {
            return `Creating Collection Amounting to <b>${toCurrency.format(this.collection.amount.replace(',', ''))}</b> with Reference Code <b>${this.collection.reference_code}</b>
            <br>
            <br>
            ${this.selectedRows.map((row) => `${row.id_display} Amount Due: <b>${toCurrency.format(row.amount)}</b><br>`).join("")}
            <br>
            Collection Results to <b>${toCurrency.format(this.calculateAP())} AP</b> and will be posted to this Account.
            `
        },
        confirmCreateCollection() {
            this.$buefy.dialog.confirm({
                title: 'Creating Collection',
                message: this.generateCollectionMessage(),
                confirmText: 'Create Collection',
                type: 'is-info',
                hasIcon: true,
                onConfirm: () => this.createCollection()
            })
        },
        async createCollection() {
            try {
                this.isLoading = true
                // construct data
                const collection = {
                    client: this.client.id,
                    reference_code: this.collection.reference_code,
                    collection_amount: this.collection.amount.replace(',', ''),
                    refundable_amount: parseFloat(this.calculateAP()).toFixed(2)
                }


                await createCollection({
                    ...collection,
                    detail: this.selectedRows.map((loan) => {
                        return {
                            content_type: 'loan_detail',
                            content_id: loan.id,
                            amount: loan.amount
                        }
                    })
                });

                this.selectedRows = []
                this.collection = {
                    reference_code: '',
                    amount: ''
                }
                this.$buefy.toast.open({
                    message: 'Collection Successfully Posted!',
                    type: 'is-success'
                })

                // Refetch Client
                this.fetchClients();
            } catch (err) {
                this.$buefy.toast.open({
                    message: `Something went wrong! ${err.message}`,
                    type: 'is-danger'
                })
            } finally {
                this.isLoading = false
            }
        },
        async processPayment () {
            try {
                this.isLoading = true
                const collection = {...this.collection}

                const data = {
                    ...collection,
                    client: this.client.id,
                    collection_amount: collection.amount.replace(',', ''),
                    post_date: moment(collection.post_date).format('YYYY-MM-DD')
                }

                await createCollection(data)

                this.collection = {}

                this.$buefy.toast.open({
                    message: 'Collection Successfully Posted!',
                    type: 'is-success'
                })

                // Refetch Client
                this.fetchClients()

                this.paymentModalActive = false
            } catch (err) {
                this.$buefy.toast.open({
                    message: `Something went wrong! ${err.message}`,
                    type: 'is-danger'
                })
            } finally {
                this.isLoading = false
            }
        }
    }
}
</script>

<style>
    .header {
        margin-bottom: 1.5em;
    }

    tr.is-success {
        background-color: #cef3ce;
    }

    .table-title {
        background-color: #def5f5;
        padding: 0.5em;
    }

    .tab-container {
        padding: 2em;
    }
</style>