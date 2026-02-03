import Link from "next/link";

import { siteConfig } from "@/config/site";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function SignInPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <SiteHeader />
      <main className="mx-auto flex w-full max-w-6xl flex-1 items-center justify-center px-6 py-16">
        <Card className="w-full max-w-md">
          <CardHeader className="space-y-2">
            <CardTitle>Welcome back</CardTitle>
            <p className="text-sm text-slate-500">
              {siteConfig.auth.note}
            </p>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="email">Work email</Label>
              <Input id="email" placeholder="name@firm.com" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" placeholder="••••••••" />
            </div>
            <Button className="w-full">Sign in</Button>
            <div className="space-y-2">
              {siteConfig.auth.providers.map((provider) => (
                <button
                  key={provider}
                  className={`${buttonVariants({ variant: "outline" })} w-full`}
                  type="button"
                >
                  Continue with {provider}
                </button>
              ))}
            </div>
            <p className="text-center text-sm text-slate-500">
              New to AFCEN?{" "}
              <Link
                href="/auth/sign-up"
                className="font-medium text-emerald-600 hover:text-emerald-700"
              >
                Request access
              </Link>
            </p>
          </CardContent>
        </Card>
      </main>
      <SiteFooter />
    </div>
  );
}
