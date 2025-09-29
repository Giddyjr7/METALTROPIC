import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"

const Signup = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background text-foreground">
      <Card className="w-full max-w-md bg-card text-card-foreground shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl font-semibold text-center">Sign Up</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input
            type="text"
            placeholder="Full Name"
            className="bg-input text-foreground border border-border"
          />
          <Input
            type="email"
            placeholder="Email"
            className="bg-input text-foreground border border-border"
          />
          <Input
            type="password"
            placeholder="Password"
            className="bg-input text-foreground border border-border"
          />
          <Input
            type="password"
            placeholder="confirm Password"
            className="bg-input text-foreground border border-border"
          />
        </CardContent>
        <CardFooter className="flex flex-col space-y-3">
          <Button className="w-full bg-primary text-primary-foreground hover:bg-primary/80">
            Create Account
          </Button>
          <p className="text-sm text-muted-foreground text-center">
            Already have an account? <a href="/login" className="text-primary hover:underline">Login</a>
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}

export default Signup
