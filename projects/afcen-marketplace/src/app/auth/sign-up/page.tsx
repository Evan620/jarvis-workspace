import Link from "next/link";

import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function SignUpPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <SiteHeader />
      <main className="mx-auto flex w-full max-w-6xl flex-1 items-center justify-center px-6 py-16">
        <Card className="w-full max-w-md">
          <CardHeader className="space-y-2">
            <CardTitle>Request investor access</CardTitle>
            <p className="text-sm text-slate-500">
              Share a few details and our team will confirm eligibility.
            </p>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Full name</Label>
              <Input id="name" placeholder="Jane Doe" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="firm">Investment firm</Label>
              <Input id="firm" placeholder="Green Ridge Capital" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Work email</Label>
              <Input id="email" placeholder="name@firm.com" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="ticket">Typical ticket size</Label>
              <Input id="ticket" placeholder="$1M - $5M" />
            </div>
            <Button className="w-full">Submit request</Button>
            <p className="text-center text-sm text-slate-500">
              Already have access?{" "}
              <Link
                href="/auth/sign-in"
                className="font-medium text-emerald-600 hover:text-emerald-700"
              >
                Sign in
              </Link>
            </p>
          </CardContent>
        </Card>
      </main>
      <SiteFooter />
    </div>
  );
}
