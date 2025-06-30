import { Zap, Search } from "lucide-react";
import { Hero } from "@/components/hero";
export default function Home() {
    return (
        <Hero
            icon={<Search className="size-6" />}
            heading="Leet-Search!!! Semantic LeetCode Search Powered by AI"
            description="Stop wasting time guessing keywords. Search LeetCode questions semantically using natural language. Get accurate matches based on meaning, not just words."
            button={{
                text: "Try Semantic Search",
                icon: <Zap className="ml-2 size-4" />,
                url: "/search",
            }}
            trustText="Used by 2,000+ developers to speed up problem solving"
            imageSrc="/image.png"
            imageAlt="AI search illustration"
        />
    );
}
