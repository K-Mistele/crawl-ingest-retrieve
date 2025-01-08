
export default async function IngestionPage({
    params,
    searchParams
}: {
    params: Promise<{}>,
    searchParams: Promise<{[key: string]: string | Array<string> | undefined}>
}) {

    const query = (await searchParams)['domain']
    if (!query) return
    return (
        <div className={'w-full h-full max-h-screen max-w-full min-h-0 grid grid-cols-3'}>

            <div className={''}>

            </div>
        </div>
    )
}