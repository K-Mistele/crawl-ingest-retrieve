'use server'
import {setTimeout} from 'node:timers/promises'

export async function createIngestion(data: FormData) {

    await setTimeout(3000)
}