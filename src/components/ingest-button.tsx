'use client'
import {Button} from '@/components/ui/button'
import {useFormStatus} from 'react-dom'
import {LoaderCircleIcon} from 'lucide-react'

export function IngestButton() {
    const status = useFormStatus()
    return (
        <Button type={'submit'} variant={'default'}>{
            status.pending
                ? <><LoaderCircleIcon className={'animate-spin mr-1'}/> Loading... </>
                : <>Ingest Domain</>
        }</Button>
    )
}