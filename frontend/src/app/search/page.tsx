'use client';

import { Suspense } from "react";
import SearchPageContent from "./searchpage";
export default function SearchPage() {
    return (
        <Suspense fallback={<div className="flex items-center justify-center h-screen">Loading...</div>}>
            <SearchPageContent />
        </Suspense>
    );
}
