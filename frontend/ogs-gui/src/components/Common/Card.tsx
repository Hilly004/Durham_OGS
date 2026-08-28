import type {
    ElementType,
    ReactNode,
} from "react";


type CardVariant =
    | "solid"
    | "soft";


interface CardProps {
    children: ReactNode;
    variant?: CardVariant;
    className?: string;
    as?: ElementType;
}


export default function Card({
    children,
    variant = "solid",
    className = "",
    as: Component = "div",
}: CardProps) {

    const variantClasses: Record<
        CardVariant,
        string
    > = {

        solid: `
            rounded-xl
            border
            border-slate-800
            bg-slate-900
        `,

        soft: `
            rounded-xl
            border
            border-slate-800
            bg-slate-900/40
            p-5
        `,

    };


    return (
        <Component
            className={`
                ${variantClasses[variant]}
                ${className}
            `}
        >
            {children}
        </Component>
    );
}