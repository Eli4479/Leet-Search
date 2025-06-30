'use client';

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import axios from "axios";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
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
    tags?: string[];
}

export default function SearchPage() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const initialPage = Number(searchParams.get("page")) || 0;

    const [query, setQuery] = useState("");
    const [questions, setQuestions] = useState<Question[]>([]);
    const [page, setPage] = useState(initialPage);
    const [loading, setLoading] = useState(false);

    // Update URL on page change
    useEffect(() => {
        const current = new URLSearchParams(Array.from(searchParams.entries()));
        current.set("page", page.toString());
        router.replace(`/search?${current.toString()}`);
    }, [page]);

    const fetchQuestions = async () => {
        if (!query.trim()) return;

        try {
            setLoading(true);
            const res = await axios.post(`http://127.0.0.1:8000/api/search?page=${page}`, {
                query,
                limit: 5,
            });

            if (!Array.isArray(res.data)) throw new Error("Invalid response format");

            setQuestions(res.data);
        } catch (err) {
            console.error("Error fetching data:", err);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = () => {
        setPage(0);
        fetchQuestions();
    };

    useEffect(() => {
        if (query) fetchQuestions();
    }, [page]);

    return (
        <div className="max-w-full mx-auto px-4 md:px-10 py-10 space-y-8">
            <div className="flex gap-4 items-center justify-between flex-col sm:flex-row">
                <Input
                    placeholder="Enter your question..."
                    value={query}
                    type="text"
                    onChange={(e) => setQuery(e.target.value)}
                    className="w-full h-24 text-lg rounded-xl px-6 py-4 shadow border border-border bg-background"
                />
                <Button
                    onClick={handleSearch}
                    className="self-stretch sm:self-auto w-full sm:w-auto text-base font-medium"
                >
                    Search
                </Button>
            </div>

            {/* Results */}
            {loading ? (
                <div className="space-y-4">
                    {[...Array(5)].map((_, idx) => (
                        <Card key={idx} className="animate-pulse">
                            <CardContent className="p-4 space-y-3">
                                <Skeleton className="h-6 w-2/3" />
                                <Skeleton className="h-4 w-full" />
                                <Skeleton className="h-4 w-3/4" />
                            </CardContent>
                        </Card>
                    ))}
                </div>
            ) : (
                <div className="w-full px-2 sm:px-4 md:px-6 py-10">
                    {questions.length > 0 ? (
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            {questions.map((q) => (
                                <Card key={q.id} className="w-full h-full shadow-md border border-border">
                                    <CardContent className="p-6 space-y-4">
                                        <div className="flex items-center flex-col justify-between md:flex-row">
                                            <a
                                                href={q.url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-xl font-semibold text-primary underline"
                                            >
                                                {q.title}
                                            </a>
                                            <p className="text-sm text-green-600 font-semibold pt-5 md:pt-0">
                                                Match: {q.match_percentage?.toFixed(2)}%
                                            </p>
                                        </div>
                                        {q.original_content && (
                                            <div
                                                className="text-base p-4 bg-muted rounded-lg border border-border transition-all duration-200 leading-relaxed overflow-x-hidden whitespace-normal break-words"
                                                dangerouslySetInnerHTML={{ __html: q.original_content }}
                                            />
                                        )}

                                        {q.tags && q.tags.length > 0 && (
                                            <div className="flex flex-wrap gap-2">
                                                {q.tags.map((tag) => (
                                                    <span
                                                        key={tag}
                                                        className="bg-primary/10 text-primary px-3 py-1 rounded-full text-sm font-medium"
                                                    >
                                                        {tag}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    ) : null}
                </div>

            )}

            {/* Pagination */}
            {questions.length > 0 && (
                <div className="pt-6 flex items-center justify-between flex-wrap gap-4">
                    <Pagination>
                        <PaginationContent>
                            <PaginationItem>
                                <PaginationPrevious
                                    onClick={() => {
                                        if (page > 0) setPage((p) => p - 1);
                                    }}
                                    className={page === 0 ? "pointer-events-none opacity-50" : ""}
                                />
                            </PaginationItem>
                            <PaginationItem>
                                <PaginationNext
                                    onClick={() => {
                                        if (questions.length > 0) setPage((p) => p + 1);
                                    }}
                                />
                            </PaginationItem>
                        </PaginationContent>
                    </Pagination>
                    <span className="text-sm text-muted-foreground">Page {page + 1}</span>
                </div>
            )}
        </div>
    );
}
