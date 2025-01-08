'use server'
import {setTimeout} from 'node:timers/promises'

export async function createIngestion(data: FormData) {

    // TODO validate that it's an example domain and strip http/s

    // TODO create ingestion task
    await setTimeout(3000)
}