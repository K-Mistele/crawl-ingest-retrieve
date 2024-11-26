'use client'
import {useToast} from '@/hooks/use-toast'
import {Input} from '@/components/ui/input'
import {Label} from '@/components/ui/label'
import {Button} from '@/components/ui/button'
import {Tooltip, TooltipContent, TooltipTrigger} from '@/components/ui/tooltip'
import Form from 'next/form'
import {createIngestion} from '@/app/actions/ingest'
import {IngestButton} from '@/components/ingest-button'

export default function Home() {
  return (
    <div className="font-[family-name:var(--font-geist-sans)] flex flex-col min-h-screen w-full items-center justify-center">

        <div className={'sm:w-full md:w-1/2 lg:w-1/3 xl:w-1/4'}>
            <Form className={'w-full flex flex-col items-start justify-center gap-2'} action={createIngestion}>
                <Label htmlFor={'domain'}>Ingestion Target</Label>
                <Input className={''} placeholder={'Enter a domain, e.g. example.com'} id={'domain'}
                       name={'domain'} type={'text'}/>
                <div className={'w-full flex flex-row-reverse'}>
                    <IngestButton/>

                </div>
            </Form>
        </div>


    </div>
  );
}
