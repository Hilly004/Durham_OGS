import type {
    ReactNode,
} from "react";


interface CardHeaderProps {
    title: string;
    subtitle?: string;
    action?: ReactNode;
    className?: string;
}


export default function CardHeader({
    title,
    subtitle,
    action,
    className = "",
}: CardHeaderProps) {

    return (
        <div
            className={`
                flex
                items-start
                justify-between
                gap-4
                border-b
                border-slate-800
                px-4
                py-3
                ${className}
            `}
        >

            <div className="min-w-0">

                <h2
                    className="
                        text-sm
                        font-semibold
                        text-slate-100
                    "
                >
                    {title}
                </h2>

                {subtitle && (
                    <p
                        className="
                            mt-1
                            text-xs
                            text-slate-400
                        "
                    >
                        {subtitle}
                    </p>
                )}

            </div>

            {action && (
                <div className="shrink-0">
                    {action}
                </div>
            )}

        </div>
    );
}