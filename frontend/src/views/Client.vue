<template>
    <div class="container is-fluid">
        <div v-if="readMode">
            <h1 class="has-text-left header is-size-4">Client Ledger</h1>
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
                <div class="column is-12">
                    <label for="">Co-Maker Full Name</label>
                    <p>{{ client.co_maker }}</p>
                </div>
            </div>
            <hr>
            <h1 class="is-size-4 has-text-left table-title">Loans and CAs</h1>
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
            <hr>
            <h1 class="is-size-4 has-text-left table-title">Collections</h1>
            <div class="columns">
                <div class="column is-12">
                    <!-- <b-table :data="collections" :columns="collectionColumns" :loading="isLoading" checkable :checked-rows.sync="selectedCollections"
                        :header-checkable="false">
                        <template #empty>
                            <div class="has-text-centered">No Results Found</div>
                        </template>
                    </b-table> -->
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
                        <b-input></b-input>
                    </b-field>
                </div>
                <div class="column is-6">
                    <b-field label="Account Number" :label-position="labelPosition">
                        <b-input></b-input>
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
                    field: 'id_display',
                    label: 'ID'
                },
                {
                    field: 'date_payment',
                    label: 'Payment Due Date',
                },
                {
                    field: 'loan_amount',
                    label: 'Principal Amount',
                    centered: true
                },
                {
                    field: 'amount',
                    label: 'Amount',
                    centered: true
                },
                {
                    field: 'balance',
                    label: 'Running Balance',
                    centered: true
                },
                {
                    field: 'is_paid',
                    label: 'Status'
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
                    payable: 0
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
</style>