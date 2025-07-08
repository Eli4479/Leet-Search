import { Zap, Search } from "lucide-react";
import { Hero } from "@/components/hero";

export default function Home() {
    return (
        <Hero
            icon={<Search className="size-6" />}
            heading="LEET SEARCH"
            subheading="Stop Guessing. Start Finding."
            description="Ever struggled to recall that one LeetCode problem you saw in an online assessment or mock test? You tried searching by random keywords, but nothing felt right. With Leet-Search, you can now search semantically — by meaning, not exact words — and instantly find the problem you're thinking of."
            button={{
                text: "Try Semantic Search",
                icon: <Zap className="ml-2 size-4" />,
                url: "/search",
            }}
            trustText="finding problems faster with AI"
            imageSrc="/image.png"
            imageAlt="AI-powered semantic LeetCode search"
        />
    );
}
