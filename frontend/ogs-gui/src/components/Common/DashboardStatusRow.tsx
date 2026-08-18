type DashboardStatusRowProps = {
    label: string;
    value: string;
    valueClassName?: string;
};


export default function DashboardStatusRow({
    label,
    value,
    valueClassName = "text-slate-300",
}: DashboardStatusRowProps) {

    return (
        <div className="flex items-center justify-between py-1.3">

            <span className="text-sm text-slate-500">
                {label}
            </span>

            <span
                className={`
                    text-sm
                    font-medium
                    ${valueClassName}
                `}
            >
                {value}
            </span>

        </div>
    );
}