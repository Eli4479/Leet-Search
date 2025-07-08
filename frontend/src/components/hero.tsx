// src/components/hero.tsx
import { Zap, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import Image from "next/image";

export interface HeroProps {
    icon?: React.ReactNode;
    heading: string;
    subheading: string; // Optional subheading
    description: string;
    button: {
        text: string;
        icon?: React.ReactNode;
        url: string;
    };
    trustText?: string;
    imageSrc?: string;
    imageAlt?: string;

}

export function Hero({
    icon = <Search className="size-6" />,
    heading = "Leet-Search!!! Semantic LeetCode Search Powered by AI",
    subheading = "Stop Guessing. Start Finding.",
    description = "Stop wasting time guessing keywords...",
    button = {
        text: "Try Semantic Search",
        icon: <Zap className="ml-2 size-4" />,
        url: "/search",
    },
    trustText = "Used by 2,000+ developers to speed up problem solving",
    imageSrc = "/image.png",
    imageAlt = "AI search illustration",
}: HeroProps) {
    return (
        <div className="flex min-h-screen items-center justify-center">
            <section className="flex flex-col items-center justify-center overflow-hidden py-32 w-full">
                <div className="container">
                    <div className="flex flex-col gap-5 items-center justify-center">
                        <div className="relative flex flex-col gap-5 items-center justify-center">
                            {/* Glowing background */}
                            <div
                                style={{
                                    transform: "translate(-50%, -50%)",
                                }}
                                className="absolute top-1/2 left-1/2 -z-10 mx-auto size-[800px] rounded-full border [mask-image:linear-gradient(to_top,transparent,transparent,white,white,white,transparent,transparent)] p-16 md:size-[1300px] md:p-32"
                            >
                                <div className="size-full rounded-full border p-16 md:p-32">
                                    <div className="size-full rounded-full border"></div>
                                </div>
                            </div>

                            {/* Icon */}
                            <span className="mx-auto flex size-16 items-center justify-center rounded-full border md:size-20">
                                {icon}
                            </span>

                            {/* Heading */}
                            <h2 className="mx-auto max-w-5xl text-center text-3xl font-medium text-balance md:text-6xl">
                                {heading}
                            </h2>

                            {/* Subheading */}
                            <h3 className="mx-auto max-w-5xl text-center text-2xl font-medium text-balance md:text-5xl">
                                {subheading}
                            </h3>

                            {/* Description */}
                            <p className="mx-auto max-w-3xl text-center text-muted-foreground md:text-lg">
                                {description}
                            </p>

                            {/* CTA */}
                            <div className="flex flex-col items-center justify-center gap-3 pt-3 pb-12">
                                <Button size="lg" asChild>
                                    <a href={button.url}>
                                        {button.text} {button.icon}
                                    </a>
                                </Button>
                                {trustText && (
                                    <div className="text-xs text-muted-foreground">
                                        {trustText}
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Image */}
                        <Image
                            src={imageSrc}
                            alt={imageAlt}
                            className="mx-auto h-full max-h-[524px] w-full max-w-5xl rounded-2xl object-contain"
                            width={1000}
                            height={524}
                            priority
                        />
                    </div>
                </div>
            </section>
        </div>
    );
}
