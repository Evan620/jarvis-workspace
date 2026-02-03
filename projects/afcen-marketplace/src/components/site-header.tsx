import Link from "next/link";

import { siteConfig } from "@/config/site";
import { buttonVariants } from "@/components/ui/button";

export function SiteHeader() {
  return (
    <header className="border-b border-slate-200/70 bg-white/80 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500 text-white font-semibold">
            AF
          </div>
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-emerald-600">
              AFCEN
            </p>
            <p className="text-lg font-semibold text-slate-900">
              Project Marketplace
            </p>
          </div>
        </div>
        <nav className="hidden items-center gap-6 text-sm font-medium text-slate-600 md:flex">
          {siteConfig.nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="transition-colors hover:text-emerald-600"
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          <Link
            href="/auth/sign-in"
            className={`${buttonVariants({ variant: "ghost" })} hidden md:inline-flex`}
          >
            Sign In
          </Link>
          <Link href="/auth/sign-up" className={buttonVariants({})}>
            Request Access
          </Link>
        </div>
      </div>
    </header>
  );
}
