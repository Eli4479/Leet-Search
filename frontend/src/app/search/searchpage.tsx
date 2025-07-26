'use client';

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { toast } from "sonner";
import axios from "axios";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge"
import {
    Pagination,
    PaginationContent,
    PaginationItem,
    PaginationPrevious,
    PaginationNext,
} from "@/components/ui/pagination";

interface Question {
    id: string;
    title: string;
    url: string;
    content: string;
    match_percentage: number;
    original_content?: string;
    paid_only?: boolean;
    difficulty?: string;
    topictags?: string;
}

export default function SearchPageContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const initialPage = Number(searchParams.get("page")) || 0;

    const [query, setQuery] = useState("");
    const [questions, setQuestions] = useState<Question[]>([]);
    const [PaginationQuestions, setPaginationQuestions] = useState<Question[]>([]);
    const [page, setPage] = useState(initialPage);
    const [loading, setLoading] = useState(false);
    const [buttonDisabled, setButtonDisabled] = useState(false);
    const [timer, setTimer] = useState(0.0);

    useEffect(() => {
        const current = new URLSearchParams(Array.from(searchParams.entries()));
        current.set("page", page.toString());
        router.replace(`/search?${current.toString()}`);
    }, [page]);

    const fetchQuestions = async () => {
        if (!query.trim()) return;
        // make a stop watch timer
        const interval = setInterval(() => {
            setTimer((prev) => Math.round((prev + 0.1) * 10) / 10);
        }, 100);
        try {
            // make a function to handle the timer
            setTimer(0);
            setLoading(true);
            setButtonDisabled(true);
            const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/search`, {
                query,
            });
            if (!Array.isArray(res.data)) throw new Error("Invalid response format");
            setQuestions(res.data);
            setPage(0); // reset page to 0 on new search
            setPaginationQuestions(res.data.slice(0, 5)); // set initial pagination
            toast.success("Search results fetched successfully!");
        } catch (err) {
            console.error("Error fetching data:", err);
            toast.error("Failed to fetch search results.");
        } finally {
            // clear the timer
            clearInterval(interval);
            setTimer(0);
            setButtonDisabled(false);
            setLoading(false);
        }
    };
    const handleGetSolution = async (id: string) => {
        try {
            window.open(`https://leetcode.doocs.org/lc/${id}`, "_blank");
        } catch (err) {
            console.error("Error navigating to solution:", err);
            toast.error("Failed to navigate to solution.");
        }
    };
    const handleSearch = () => {
        fetchQuestions();
    };

    useEffect(() => {
        if (query.trim()) {
            setPaginationQuestions(
                questions.slice(page * 5, (page + 1) * 5)
            );
        }
    }, [page]);
    return (
        <div className="max-w-full mx-auto px-4 md:px-10 py-10 space-y-8">
            <div className="flex gap-4 items-center justify-between flex-col sm:flex-row">
                <Input
                    placeholder="Enter your question..."
                    value={query}
                    type="text"
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            e.preventDefault();
                            handleSearch();
                        }
                    }}
                    className="w-full h-24 text-lg rounded-xl px-6 py-4 shadow border border-border bg-background"
                />
                <Button
                    onClick={handleSearch}
                    className="self-stretch sm:self-auto w-full sm:w-auto text-base font-medium"
                    disabled={buttonDisabled || loading}
                >
                    Search
                </Button>
            </div>
            {loading ? (
                <>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {[...Array(5)].map((_, idx) => (
                            <Card key={idx} className="animate-pulse w-full h-full shadow-md border border-border">
                                <CardContent className="p-6 space-y-4">
                                    <div className="flex items-center flex-col justify-between md:flex-row">
                                        <Skeleton className="h-6 w-1/3" />
                                        <Skeleton className="h-4 w-16 mt-4 md:mt-0" />
                                    </div>
                                    <Skeleton className="h-4 w-full" />
                                    <Skeleton className="h-4 w-4/5" />
                                    <Skeleton className="h-4 w-3/5" />
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                    <div className="text-center text-sm text-muted-foreground mt-4">
                        Loading... {timer.toFixed(1)} seconds
                    </div>
                </>
            ) : (
                <div className="w-full px-2 sm:px-4 md:px-6 py-10">
                    {PaginationQuestions.length > 0 && (
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            {PaginationQuestions.map((q) => (
                                <Card key={q.id} className="w-full h-full shadow-md border border-border">
                                    <CardContent className="p-6 space-y-4">
                                        <div className="flex flex-col md:flex-row md:justify-between justify-start">
                                            <div>
                                                <a
                                                    href={q.url}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    className="text-xl font-semibold text-primary hover:underline"
                                                >
                                                    {q.id}. {q.title}
                                                </a>
                                                {q.paid_only && (
                                                    <span className="text-xl ml-2">
                                                        🔒
                                                    </span>
                                                )}
                                            </div>
                                            <p className="text-md text-green-600 font-semibold py-5 md:pt-0">
                                                Match: {q.match_percentage?.toFixed(2)}%
                                            </p>
                                            <p className="text-md text-muted-foreground">
                                                {q.difficulty === "Easy" ? (
                                                    <Badge variant="easy">Easy</Badge>
                                                ) : q.difficulty === "Medium" ? (
                                                    <Badge variant="medium">Medium</Badge>
                                                ) : q.difficulty === "Hard" ? (
                                                    <Badge variant="hard">Hard</Badge>
                                                ) : (
                                                    <Badge>Unknown</Badge>
                                                )}
                                            </p>
                                        </div>
                                        <Button
                                            variant="solution"
                                            onClick={() => handleGetSolution(q.id)}
                                        >Get Solution</Button>
                                        {q.original_content && (
                                            <div
                                                className="text-base p-4 bg-muted rounded-lg border border-border transition-all duration-200 leading-relaxed overflow-x-hidden whitespace-normal break-words"
                                                dangerouslySetInnerHTML={{ __html: q.original_content }}
                                            />
                                        )}
                                        {q.topictags && (
                                            <div className="flex flex-wrap gap-2 mt-2">
                                                {q.topictags.split("@").map((tag, index) => (
                                                    <Badge key={index} variant="tags">
                                                        {tag.trim()}
                                                    </Badge>
                                                ))}
                                            </div>
                                        )}
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    )}
                </div>
            )
            }

            {
                questions.length > 0 && (
                    <div className="pt-6 flex items-center justify-between flex-wrap gap-4">
                        <Pagination>
                            <PaginationContent>
                                <PaginationItem>
                                    <PaginationPrevious
                                        onClick={() => {
                                            if (questions.length > 0) setPage((p) => p - 1);
                                        }}
                                        className={page === 0 ? "pointer-events-none opacity-50" : ""}
                                    />
                                </PaginationItem>
                                <PaginationItem>
                                    <PaginationNext
                                        onClick={() => {
                                            if (questions.length > 0) setPage((p) => p + 1);
                                        }}
                                        className={questions.length <= (page + 1) * 5 ? "pointer-events-none opacity-50" : ""}
                                    />
                                </PaginationItem>
                            </PaginationContent>
                        </Pagination>
                        <span className="text-sm text-muted-foreground">Page {page + 1}</span>
                    </div>
                )
            }
        </div >
    );
}
